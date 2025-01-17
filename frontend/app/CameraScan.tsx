// import react and other necessary modules from react-native
import React, { useState } from "react";
import {
  View,
  Text,
  Alert,
  StyleSheet,
  TouchableOpacity,
  Linking,
} from "react-native";
// import icon for camera flip button
import { Ionicons } from "@expo/vector-icons";
// import necessary modules from expo-camera
import { CameraView, useCameraPermissions, CameraType } from "expo-camera";

// CameraScan component
export default function CameraScan() {
  // use state to store and manage camera permission
  const [hasPermission, requestPermission] = useCameraPermissions();
  // use state to store and manage camera type (front or back)
  const [cameraType, setCameraType] = useState<CameraType>("back");
  // use state to store and manage scanning status
  const [isScanning, setIsScanning] = useState(true);

  // handling when camera permissions have not yet loaded (based on expo-camera documentation: https://docs.expo.dev/versions/latest/sdk/camera/)
  if (!hasPermission) {
    return (
      <View style={styles.container}>
        <Text>Camera permissions are still loading...</Text>
      </View>
    );
  }

  // handling when camera permissions are not yet granted (based on expo-camera documentation: https://docs.expo.dev/versions/latest/sdk/camera/)
  if (!hasPermission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>
          We need your permission to use the camera
        </Text>
        {/* adding button so that user can grant permission */}
        <TouchableOpacity onPress={requestPermission} style={styles.button}>
          <Text style={styles.text}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  // handling qr code scanning
  const handleQrCodeScanned = ({ data }: { data: string }) => {
    // stop scanning
    setIsScanning(false);
    // check for link
    if (!data.startsWith("http://") && !data.startsWith("https://")) {
      Alert.alert("No URL Found", "This is not a Quishing Attempt!");
      return;
    }

    // send link to backend
    fetch("http://localhost:5000/validate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: data }),
    })
      // handle response from backend (quishing or not)
      .then((response) => response.json())
      .then((result) => {
        if (result.result === "bad") {
          Alert.alert(
            "Oh no! This website has been deemed malicious. Best to give it a miss!"
          );
        } else {
          Alert.alert(
            "Safe!",
            "This QR code looks safe! Would you like to proceed to the webpage?",
            [
              { text: "No", style: "cancel" },
              { text: "Yes", onPress: () => Linking.openURL(data) },
            ]
          );
        }
      })
      // if there is an error, log the error and show an alert for the user
      .catch((error) => {
        console.error("Error:", error);
        Alert.alert("Error", "Unable to validate the QR code at the moment.");
      });
  };

  return (
    <View style={styles.container}>
      {/* camera view */}
      <CameraView
        style={styles.camera}
        facing={cameraType}
        onBarcodeScanned={isScanning ? handleQrCodeScanned : undefined}
        barcodeScannerSettings={{
          barcodeTypes: ["qr"],
        }}
      />
      {/* button to switch camera type (front/back) */}
      <TouchableOpacity
        style={styles.flipButton}
        onPress={() =>
          setCameraType((prev) => (prev === "back" ? "front" : "back"))
        }
      >
        <Ionicons name="camera-reverse" size={24} color="#fff" />
      </TouchableOpacity>
    </View>
  );
}

// styles for the CameraScan component
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  message: {
    fontSize: 16,
    textAlign: "center",
  },
  button: {
    marginTop: 10,
    padding: 10,
    backgroundColor: "#007bff",
    borderRadius: 5,
  },
  text: {
    color: "#fff",
    fontSize: 16,
  },
  camera: {
    flex: 1,
    width: "100%",
  },
  flipButton: {
    position: "absolute",
    bottom: 30,
    padding: 10,
    backgroundColor: "#007bff",
    borderRadius: 5,
  },
});
