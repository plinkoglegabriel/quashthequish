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

  // handling when camera permissions have not yet loaded (based on expo-camera documentation)
  if (!hasPermission) {
    return (
      <View style={styles.container}>
        <Text>Camera permissions are still loading...</Text>
      </View>
    );
  }

  // handling when camera permissions are not yet granted (based on expo-camera documentation)
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

  return <View style={styles.container} />;
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
});
