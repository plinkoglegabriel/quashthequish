// import react and other necessary modules from react-native
import React, { useState, useRef } from "react";
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
// import useNavigation hook from react-navigation
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "../types";
import { DEVICE_ADDRESS } from "../config";

// CameraScan component
export default function CameraScan() {
  // use state to store and manage camera permission
  const [hasPermission, requestPermission] = useCameraPermissions();
  // use state to store and manage camera type (front or back)
  const [cameraType, setCameraType] = useState<CameraType>("back");
  // get navigation prop
  const navigation = useNavigation<StackNavigationProp<RootStackParamList>>();
  // store device IP address from local file
  const device = DEVICE_ADDRESS;
  // preventing multiple scans
  const isScanning = useRef(true);
  // preventing multiple alerts
  const alertShown = useRef(false);

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

  // handling QR code scanning
  const handleQrCodeScanned = async ({ data }: { data: string }) => {
    // if scanning is disabled or alert is already shown, return (this prevents multiple scans and alerts)
    if (!isScanning.current || alertShown.current) return;

    // setting scanning to false and alertShown to true (logic again to prevent multiple scans and alerts)
    isScanning.current = false;
    alertShown.current = true;

    // // if data does not start with http:// or https://, show alert that the qr code does not contain a URL and is therefore not a quishing attempt
    if (!data.startsWith("http://") && !data.startsWith("https://")) {
      Alert.alert("No URL Found!", "This is not a Quishing Attempt!", [
        {
          text: "OK",
          // after user has accepted the alert, set scanning to true and alertShown to false
          onPress: () => {
            isScanning.current = true;
            alertShown.current = false;
          },
        },
      ]);
      return;
    }

    // try to send a POST request to the backend to validate the URL
    try {
      const response = await fetch(`http://${device}:5001/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: data }),
      });

      // handle response from backend (quishing or not)
      // if response is not ok, log the error and throw an error
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend error:", errorText);
        throw new Error(`Network response was not ok: ${errorText}`);
      }
      // return json response from backend
      const result = await response.json();
      console.log("Raw response:", result);

      // if the result is bad, show an alert that the website has been deemed malicious
      // if the result is good, show an alert that the website is safe and ask the user if they want to proceed
      if (result.result === "bad") {
        const alertMessages: {
          title: string;
          message: string;
          buttonText?: string;
        }[] = [];

        // push the "malicious" alert
        alertMessages.push({
          title: "Oh no!",
          message: "This website has been deemed malicious.",
          buttonText: "Okay",
        });

        // if the result is bad but the user has discovered url (i.e its not already in the database), send a congratulations message
        if (result.newQuish) {
          alertMessages.push({
            title: "On the other hand...Congrats 🎉!",
            message:
              "You are the first to find this Quishing attempt! Check the leaderboard to see your new score!",
            buttonText: "Yay me!",
          });
        }

        const showQuishAlerts = (index = 0) => {
          if (index >= alertMessages.length) {
            // after user has accepted the alert/s, set scanning to true and alertShown to false
            isScanning.current = true;
            alertShown.current = false;
            return;
          }

          const current = alertMessages[index];
          Alert.alert(current.title, current.message, [
            {
              text: current.buttonText,
              onPress: () => showQuishAlerts(index + 1),
            },
          ]);
        };

        showQuishAlerts();
      } else if (result.result === "safe") {
        Alert.alert(
          "Safe!",
          "This QR code looks safe! Would you like to proceed?",
          [
            {
              text: "No",
              onPress: () => {
                isScanning.current = true;
                alertShown.current = false;
              },
              style: "cancel",
            },
            {
              text: "Yes",
              // if user clicks yes, open the URL in their default browser
              onPress: () => {
                alertShown.current = false;
                Linking.openURL(data);
              },
            },
          ]
        );
      }
      // catch any errors that occur during the fetch request and alert the user the QR code could not be validated
    } catch (error) {
      console.error("Error:", error);
      Alert.alert("Error", "Unable to validate the QR code.", [
        {
          // after user has accepted the alert, set scanning to true and alertShown to false
          text: "OK",
          onPress: () => {
            isScanning.current = true;
            alertShown.current = false;
          },
        },
      ]);
    }
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
      {/* back button */}
      <TouchableOpacity
        style={styles.backButton}
        onPress={() => navigation.goBack()}
      >
        <Ionicons name="arrow-back" size={24} color="#fff" />
      </TouchableOpacity>
      {/* button to switch camera type (front/back) */}
      <TouchableOpacity
        testID="flipButton"
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
    backgroundColor: "#000000",
    borderRadius: 5,
  },
  backButton: {
    position: "absolute",
    top: 70,
    left: 20,
    padding: 10,
    backgroundColor: "#000000",
    borderRadius: 5,
  },
});
