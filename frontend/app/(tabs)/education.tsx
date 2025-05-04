// Import necessary modules
import React from "react";
import {
  View,
  Text,
  ActivityIndicator,
  ScrollView,
  Image,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useFonts } from "expo-font";
import * as Linking from "expo-linking";

// User education screen
export default function EducationScreen() {
  // Load custom font for the app using useFonts hook
  const [fontsLoaded] = useFonts({
    Michroma: require("../../assets/fonts/Michroma-Regular.ttf"),
  });

  if (!fontsLoaded) {
    return <ActivityIndicator size="large" color="#ffffff" />;
  }

  // content to be displayed as safety tips in a ScrollView component
  const safetyTips = [
    {
      id: "1",
      title: "Avoiding Qushing",
      description:
        "Understand how QR codes work and how to stay safe when scanning them.",
      link: "https://www.scam-detector.com/quishing/",
      image: require("../../assets/images/qr-codes.png"),
    },
    {
      id: "2",
      title: "Phishing Awareness",
      description:
        "Learn how to spot fake emails and messages that are attempting to steal your data.",
      link: "https://www.phishing.org/what-is-phishing",
      image: require("../../assets/images/phishing.jpg"),
    },
  ];

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={[styles.heading1, { fontFamily: "Michroma" }]}>
          Staying Safe Online
        </Text>
        <Text style={[styles.heading2, { fontFamily: "Michroma" }]}>
          Tips and resources to help you stay safe online.
        </Text>
      </View>
      {/* ScrollView to display the list of helpful articles*/}
      <ScrollView style={styles.scrollContainer}>
        {safetyTips.map((tip) => (
          <View key={tip.id} style={styles.tip}>
            <Image source={tip.image} style={styles.image} />
            <Text style={styles.title}>{tip.title}</Text>
            <Text style={styles.description}>{tip.description}</Text>
            {/* Allows users to click on the links to the articles */}
            <TouchableOpacity onPress={() => Linking.openURL(tip.link)}>
              <Text style={styles.link}>Learn More</Text>
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "black",
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 15,
  },

  heading1: {
    fontSize: 30,
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },

  headerContainer: {
    marginTop: 100,
  },

  heading2: {
    fontSize: 19,
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
    margin: 10,
  },
  paragraph: {
    fontSize: 16,
    color: "#cccccc",
    textAlign: "center",
  },
  scrollContainer: {
    marginTop: 20,
    flexGrow: 1,
  },
  tip: {
    backgroundColor: "#1e1e1e",
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    alignItems: "center",
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 10,
    marginBottom: 10,
  },
  title: {
    fontSize: 18,
    color: "#ffffff",
    fontWeight: "bold",
    marginBottom: 5,
  },
  description: {
    fontSize: 14,
    color: "#cccccc",
    textAlign: "center",
    marginBottom: 10,
  },
  link: {
    fontSize: 14,
    color: "#1e90ff",
    fontWeight: "bold",
  },
});
