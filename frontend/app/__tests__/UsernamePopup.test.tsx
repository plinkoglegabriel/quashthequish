// importing necessary modules
import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react-native";
import UsernamePopup from "../../components/UsernamePopup";

// mocking global fetch for username check
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ exists: false }),
  })
) as jest.Mock;

// mocking js-cookie
jest.mock("js-cookie", () => ({
  get: jest.fn(),
  set: jest.fn(),
}));

// testing the UsernamePopup component
describe("UsernamePopup", () => {
  it("usernamepopup is rendered and a new username is submitted", async () => {
    // create mock of the setUsername function
    const setUsernameFunctionMock = jest.fn();

    // render the UsernamePopup component
    const { getByPlaceholderText, getByText } = render(
      <UsernamePopup visible={true} onUsernameSet={setUsernameFunctionMock} />
    );
    // set input to "testuser"
    const userInput = getByPlaceholderText("Username");
    fireEvent.changeText(userInput, "testuser");

    // simulate submitting the testuser username (via pressing submit button)
    const button = getByText("Submit");
    fireEvent.press(button);

    // check if the fetch function was called with the correct local host URL (contianing "/check-username" and the correct username)
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/check-username"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ username: "testuser" }),
        })
      );
      // check if the mocked setUsername function was called with the correct username
      expect(setUsernameFunctionMock).toHaveBeenCalledWith("testuser");
    });
  });
});
