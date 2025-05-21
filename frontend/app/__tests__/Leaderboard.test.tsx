// importing necessary modules
import React from "react";
import { render, waitFor } from "@testing-library/react-native";
import TabTwoScreen from "../(tabs)/leaderboard";
import Cookies from "js-cookie";

// mocking global fetch for leaderboard and user data
global.fetch = jest.fn((localHostUrl) => {
  // checking if request URL contains "/leaderboard" and if so, returning mock leaderboard data
  if (localHostUrl?.toString().includes("/leaderboard")) {
    return Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve([
          { username: "user1", num_of_links: 5 },
          { username: "user2", num_of_links: 3 },
        ]),
    });
    // checking if request URL contains "/userData/testuser" and if so, returning mock ranking data
  } else if (localHostUrl?.toString().includes("/userData/testuser")) {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ ranking: 1 }),
    });
  }
  // return a resolved (empty) promise for any other request url
  return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
}) as jest.Mock;

// mocking js-cookie
jest.mock("js-cookie", () => ({
  get: jest.fn(() => "testuser"),
}));

// Mock font loading
jest.mock("expo-font", () => ({
  useFonts: () => [true],
}));

// mocking the useFocusEffect function
jest.mock("@react-navigation/native", () => ({
  useFocusEffect: (cb: () => void) => {
    cb();
  },
}));

describe("TabTwoScreen", () => {
  it("leaderboard is rendered and user ranking is displayed correctly", async () => {
    // check expected text is rendered
    const { getByText } = render(<TabTwoScreen />);
    await waitFor(() => {
      expect(getByText("User Leaderboard")).toBeTruthy();
      expect(getByText("You are in 1st place!")).toBeTruthy();
      expect(getByText("user1")).toBeTruthy();
      expect(getByText("5")).toBeTruthy();
      expect(getByText("user2")).toBeTruthy();
      expect(getByText("3")).toBeTruthy();
    });
  });
});
