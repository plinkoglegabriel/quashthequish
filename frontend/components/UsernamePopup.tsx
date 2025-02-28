// Importing necessary libraries and tools
import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet, Modal } from "react-native";
import axios from "axios";
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
      const response = await axios.post(
        `http://${DEVICE_ADDRESS}:5001/check-username`,
        { username }
      );
      // if username is already in use then display error message to the user
      if (response.data.exists) {
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
        <Text style={styles.title}>Please enter a username</Text>
        <TextInput
          style={styles.input}
          value={username}
          onChangeText={setUsername}
          placeholder="Username"
        />
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Button title="Submit" onPress={checkUsername} />
      </View>
    </Modal>
  );
};

// styles for the UsernamePopup component
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "black",
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
  },
  error: {
    color: "red",
    marginBottom: 10,
  },
});

export default UsernamePopup;
