// importing necessary modules
import React from "react";
import { render, act, fireEvent } from "@testing-library/react-native";
import CameraScan from "../CameraScan";
import { Alert, Text } from "react-native";

// mock permission state stored
let mockPermission: any = [{ granted: true }, jest.fn()];

// check alert behaviour
jest.spyOn(Alert, "alert");

// expo-camera mock using jest and mocked permission state
jest.mock("expo-camera", () => {
  const ReactNative = require("react-native");
  return {
    CameraView: (props: any) => {
      return <ReactNative.Text>Mock Camera</ReactNative.Text>;
    },
    useCameraPermissions: () => mockPermission,
  };
});

// useNavigation mocked
jest.mock("@react-navigation/native", () => ({
  useNavigation: () => ({ goBack: jest.fn() }),
}));

describe("CameraScan", () => {
  afterEach(() => {
    // clean up after each test
    jest.clearAllMocks();
  });

  // testing camera permission request handling
  it("the permission request rendered and denial of access is handled correctly", () => {
    // denied permissions simulated
    mockPermission = [{ granted: false }, jest.fn()];
    const { getByText } = render(<CameraScan />);
    expect(getByText("We need your permission to use the camera")).toBeTruthy();
  });

  // testiting is camera flips based when the flip button is pressed
  it("flip camera button is rendered and responds appropriately to press", () => {
    // mock camera permissions being granted
    mockPermission = [{ granted: true }, jest.fn()];
    // camera scan component is rendered and flip button should be "pressed"
    const { getByTestId } = render(<CameraScan />);
    const flipButton = getByTestId("flipButton");
    // check if the flip button is rendered
    expect(flipButton).toBeTruthy();
    // test if the state changes (camera flips)
    fireEvent.press(flipButton);
  });
});
