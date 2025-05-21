// importing necessary modules
import React from "react";
import { render, act, fireEvent } from "@testing-library/react-native";
import CameraScan from "../CameraScan";
import { Alert, Text } from "react-native";

// mock permission state stored
let mockPermission: any = [{ granted: true }, jest.fn()];

// check alert behaviour
jest.spyOn(Alert, "alert");

// container to store the scan simulation
let currentScanSimulation: any = null;

// expo-camera mock using jest and mocked permission state
jest.mock("expo-camera", () => {
  const ReactNative = require("react-native");
  return {
    CameraView: (props: any) => {
      currentScanSimulation = props.onBarcodeScanned;
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

  // testing QR code scanning (bad QR code)
  it("handles the scanning of a bad QR code as expected", async () => {
    // mocking the global fetch function
    global.fetch = jest.fn(() =>
      // getting the fetch to return a promise of objects
      Promise.resolve({
        ok: true,
        // simulating a bad QR code response (without network request)
        json: () => Promise.resolve({ result: "bad", newQuish: false }),
      })
    ) as jest.Mock;

    // rendering the CameraScan component
    render(<CameraScan />);
    // simulating the QR code scan (using the mocked function)
    await act(async () => {
      await currentScanSimulation({ data: "https://malicious.com" });
    });

    // expected alert to be shown
    expect(Alert.alert).toHaveBeenCalledWith(
      "Oh no!",
      "This website has been deemed malicious.",
      // any array of buttons/actions accepted in alert
      expect.any(Array)
    );
  });
});
