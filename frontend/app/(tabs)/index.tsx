import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Image,
  ActivityIndicator,
} from "react-native";
import { useFonts } from "expo-font";
import { Ionicons } from "@expo/vector-icons";
import { styles } from "../../styles";

export default function HomeScreen() {
  const [fontsLoaded] = useFonts({
    Michroma: require("../../assets/fonts/Michroma-Regular.ttf"),
  });

  if (!fontsLoaded) {
    return <ActivityIndicator size="large" color="#ffffff" />;
  }

  return (
    <View style={styles.container}>
      <Text style={[styles.slogan, { fontFamily: "Michroma" }]}>
        Hello ______!
      </Text>
      <Image
        source={require("../../assets/images/quash-the-quish-logo.png")}
        style={styles.image}
      />
      <Text style={[styles.slogan, { fontFamily: "Michroma" }]}>
        Scan or Upload to Test your QR Code
      </Text>
      <View style={styles.actionsContainer}>
        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="camera-outline" size={40} color="white" />
          <Text style={[styles.buttonText, { fontFamily: "Michroma" }]}>
            Camera
          </Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="cloud-upload-outline" size={40} color="white" />
          <Text style={[styles.buttonText, { fontFamily: "Michroma" }]}>
            Upload
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
