// Import necessary modules
import React, { useState } from "react";
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
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "../../types";

// Import username popup
import UsernamePopup from "../../components/UsernamePopup";

// Define navigation prop's type
type NavigationProp = StackNavigationProp<RootStackParamList>;

// HomeScreen component
export default function HomeScreen() {
  // Load custom font for the app using useFonts hook
  const [fontsLoaded] = useFonts({
    Michroma: require("../../assets/fonts/Michroma-Regular.ttf"),
  });
  // Getting navigation prop from useNavigation hook
  const navigation = useNavigation<NavigationProp>();

  // State to store username
  const [username, setUsername] = useState("");

  // If fonts are not loaded, show an loading indicator
  if (!fontsLoaded) {
    return <ActivityIndicator size="large" color="#ffffff" />;
  }

  return (
    // Home screen render
    <View style={styles.container}>
      <UsernamePopup visible={!username} onUsernameSet={setUsername} />
      <Text style={[styles.heading2, { fontFamily: "Michroma" }]}>
        Hello {username}!
      </Text>
      {/* Displaying logo */}
      <Image
        source={require("../../assets/images/quash-the-quish-logo.png")}
        style={styles.image}
      />
      {/* Displaying button to scan */}
      <Text style={[styles.heading2, { fontFamily: "Michroma" }]}>
        Scan or Upload to Test your QR Code
      </Text>
      <View style={styles.actionsContainer}>
        {/* Handling logic to CameraScan */}
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate("CameraScan")}
        >
          {/* Camera Icon */}
          <Ionicons name="camera-outline" size={40} color="white" />
          <Text style={[styles.buttonText, { fontFamily: "Michroma" }]}>
            Camera
          </Text>
        </TouchableOpacity>
        {/* Handling logic to UploadScreen (template for now) */}
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
