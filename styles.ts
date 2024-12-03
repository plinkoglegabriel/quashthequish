import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: 'black',
      alignItems: 'center',
      justifyContent: 'center',
      paddingHorizontal: 15,
    },
    slogan: {
      fontSize: 19,
      color: 'white',
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 50,
    },
    actionsContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: '60%',
    },
    actionButton: {
      alignItems: 'center',
    },
    buttonText: {
      color: 'white',
      marginTop: 8,
      fontSize: 16,
    },
    image: {
      width: 400,
      height: 250,
      padding: 10,
    },
  });
  