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

  // getting data from leaderboard function in app.py
  const fetchLeaderboardData = async (device: string, setData: Function) => {
    try {
      const response = await fetch(`http://${device}:5001/leaderboard`);
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // getting username from cookies
  const fetchUserData = async (
    device: string,
    setRanking: Function,
    username?: string
  ) => {
    if (!username) return;

    // using username to fetch data from userData/<username> function in app.py
    try {
      const response = await fetch(
        `http://${DEVICE_ADDRESS}:5001/userData/${username}`
      );
      const data = await response.json();
      console.log("User data response:", data);
      // setting ranking to ranking fetched from backend
      if (data && data.ranking !== undefined) {
        setRanking(data.ranking);
      } else {
        console.error("User ranking not found.");
      }
    } catch (error) {
      console.error("Error fetching user stats:", error);
    }
  };

  // using useFocusEffect instead of useEffect to fetch data so that data updates each time the leaderboard is shown
  useFocusEffect(
    // using useCallback to prevent unnecessary re-renders
    React.useCallback(() => {
      async function fetchData() {
        await fetchLeaderboardData(device, setLeaderboardData);
        const username = Cookies.get("username");
        await fetchUserData(device, setRanking, username);
        setLoading(false);
      }
      fetchData();
    }, [])
  );

  function getOrdinalSuffix(rank: number): string {
    const rankingStr = rank.toString();
    // getting last digit of the ranking
    const lastDigit = rankingStr.slice(-1);
    // getting the two last digit of the ranking
    const lastTwoDigits = rankingStr.slice(-2);
    // check if digit is 1, 2, or 3 and not 11, 12 or 13 to assign suffix accordingly
    if (lastDigit === "1" && lastTwoDigits != "11") return "st";
    if (lastDigit === "2" && lastTwoDigits != "12") return "nd";
    if (lastDigit === "3" && lastTwoDigits != "13") return "rd";
    return "th";
  }

  // store ordinal suffix
  const ordinalSuffix = ranking !== null ? getOrdinalSuffix(ranking) : "";

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
          {ranking !== null
            ? `You are in ${ranking}${ordinalSuffix} place!`
            : "Find your ranking!"}
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
