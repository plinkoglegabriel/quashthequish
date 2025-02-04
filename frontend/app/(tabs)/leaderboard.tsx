import React from "react";
import { View, Text, ActivityIndicator, FlatList } from "react-native";
import { useFonts } from "expo-font";
import { styles } from "../../styles";

export default function TabTwoScreen() {
  const [fontsLoaded] = useFonts({
    Michroma: require("../../assets/fonts/Michroma-Regular.ttf"),
  });

  const placeholderData = [
    { id: "1", username: "User 1", points: 100 },
    { id: "2", username: "User 2", points: 200 },
    { id: "3", username: "User 3", points: 300 },
  ];

  if (!fontsLoaded) {
    return <ActivityIndicator size="large" color="#ffffff" />;
  }

  const renderItem = ({
    item,
  }: {
    item: { id: string; username: string; points: number };
  }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.username}</Text>
      <Text style={styles.cell}>{item.points}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={[styles.heading1, { fontFamily: "Michroma" }]}>
          Leaderboard
        </Text>
        <Text style={[styles.heading2, { fontFamily: "Michroma" }]}>
          You are in _____th place!
        </Text>
      </View>
      <FlatList
        style={styles.leaderboard}
        data={placeholderData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
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
