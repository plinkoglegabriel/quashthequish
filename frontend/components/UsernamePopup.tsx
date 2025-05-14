// Importing necessary libraries and tools
import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Modal,
  Image,
} from "react-native";
import Cookies from "js-cookie";

// Importing device's ip address from config file
import { DEVICE_ADDRESS } from "../config";

// Creating a UsernamePopupProps interface
interface UsernamePopupProps {
  // prop to hold whether the popup is visible or not
  visible: boolean;
  // prop to hold the function to set the username
  onUsernameSet: (username: string) => void;
}

// UsernamePopup functional component that that takes in visible and onUsernameSet props
const UsernamePopup: React.FC<UsernamePopupProps> = ({
  visible,
  onUsernameSet,
}) => {
  // useState hooks
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  // useEffect hook that checks if username is saved in cookies
  useEffect(() => {
    const savedUsername = Cookies.get("username");
    // if username is saved then username is set
    if (savedUsername) {
      onUsernameSet(savedUsername);
    }
  }, []);

  // store IP address from local file in device variable
  const device = DEVICE_ADDRESS;

  // checkUsername function that checks if username is already in use (in the database)
  const checkUsername = async () => {
    try {
      const response = await fetch(`http://${device}:5001/check-username`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username }),
      });

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Response:", data);

      // if username is already in use then display error message to the user
      if (data.exists) {
        setError("Username already in use. Please choose another one.");
      } else {
        // if not, username is set and stored in cookies for a year
        Cookies.set("username", username, { expires: 365 });
        onUsernameSet(username);
      }
    } catch (error) {
      // DEBUGGING
      console.error("Error checking username:", error);
      setError("Error checking username. Please try again.");
    }
  };

  return (
    // Modal that pops up when the user enters the application
    <Modal visible={visible} transparent={true} animationType="slide">
      <View style={styles.container}>
        {/* Displaying logo */}
        <Image
          source={require("../assets/images/quash-the-quish-logo.png")}
          style={styles.image}
        />
        <Text style={styles.title}>Please enter a username</Text>
        <TextInput
          style={styles.input}
          value={username}
          onChangeText={setUsername}
          placeholder="Username"
        />
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <TouchableOpacity style={styles.submitButton} onPress={checkUsername}>
          <Text style={styles.submitButtonText}>Submit</Text>
        </TouchableOpacity>
      </View>
    </Modal>
  );
};

// styles for the UsernamePopup component
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "center",
    backgroundColor: "black",
    paddingTop: 175,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
    color: "white",
  },
  input: {
    width: "80%",
    padding: 10,
    backgroundColor: "white",
    marginBottom: 10,
    borderRadius: 10, // curved corners
  },
  error: {
    color: "red",
    marginBottom: 10,
  },
  submitButton: {
    backgroundColor: "white",
    paddingVertical: 10,
    paddingHorizontal: 30,
    borderRadius: 10,
    marginTop: 10,
  },
  submitButtonText: {
    color: "black",
    fontSize: 16,
    fontWeight: "bold",
  },
  image: {
    width: 300,
    height: 180,
    padding: 10,
  },
});

export default UsernamePopup;
