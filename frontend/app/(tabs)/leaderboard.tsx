import React, { useState } from "react";
import { useFocusEffect } from "@react-navigation/native";
import { View, Text, ActivityIndicator, FlatList } from "react-native";
import { useFonts } from "expo-font";
import { styles } from "../../styles";
import { DEVICE_ADDRESS } from "../../config";
import Cookies from "js-cookie";

// Interface for leaderboard data
interface LeaderboardEntry {
  username: string;
  num_of_links: number;
}

export default function TabTwoScreen() {
  const [fontsLoaded] = useFonts({
    Michroma: require("../../assets/fonts/Michroma-Regular.ttf"),
  });
  // states to store leaderboard data and loading status
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardEntry[]>(
    []
  );
  const [ranking, setRanking] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  // store device IP address from local file
  const device = DEVICE_ADDRESS;

  // using useFocusEffect instead of useEffect to fetch data so that data updates each time the leaderboard is shown
  useFocusEffect(
    // using useCallback to prevent unnecessary re-renders
    React.useCallback(() => {
      async function fetchData() {
        await fetchLeaderboardData();
        await fetchUserData();
        setLoading(false);
      }
      fetchData();
    }, [])
  );

  // getting data from leaderboard function in app.py
  const fetchLeaderboardData = async () => {
    try {
      const response = await fetch(`http://${device}:5001/leaderboard`);
      const data = await response.json();
      setLeaderboardData(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // getting username from cookies
  const fetchUserData = async () => {
    const username = Cookies.get("username");
    if (!username) return;

    // using username to fetch data from userData/<username> function in app.py
    try {
      const response = await fetch(
        `http://${DEVICE_ADDRESS}:5001/userData/${username}`
      );
      const data = await response.json();
      console.log("User data response:", data);
      // setting ranking to ranking fetched from backend
      setRanking(data.ranking);
    } catch (error) {
      console.error("Error fetching user stats:", error);
    }
  };

  if (!fontsLoaded) {
    return <ActivityIndicator size="large" color="#ffffff" />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={[styles.heading1, { fontFamily: "Michroma" }]}>
          User Leaderboard
        </Text>
        <Text style={[styles.heading2, { fontFamily: "Michroma" }]}>
          {`You are in ${ranking}th place`}
        </Text>
      </View>
      <FlatList
        style={styles.leaderboard}
        data={leaderboardData}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <Text style={styles.cell}>{item.username}</Text>
            <Text style={styles.cell}>{item.num_of_links}</Text>
          </View>
        )}
        keyExtractor={(item, index) => index.toString()}
        ListHeaderComponent={
          <View style={styles.row}>
            <Text style={styles.cell}>Username</Text>
            <Text style={styles.cell}>QR Codes Found</Text>
          </View>
        }
      />
    </View>
  );
}
