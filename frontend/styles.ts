import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: 'black',
      alignItems: 'center',
      justifyContent: 'center',
      paddingHorizontal: 15,
    },

    heading1: {
      fontSize: 30,
      color: 'white',
      fontWeight: 'bold',
      textAlign: 'center',
    },

    heading2: {
      fontSize: 19,
      color: 'white',
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 50,
    },

    heading3: {
      fontSize: 15,
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
      width: 390,
      height: 250,
      padding: 10,
    },
    headerContainer: {
      marginTop: 100,
    },

    // leaderboard table styling
    row: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      padding: 10,
      borderBottomWidth: 1,
      borderBottomColor: 'white',
    },
    cell: {
      color: 'white',
      fontSize: 16,
    },
    leaderboard: {
      width: '80%',
    },
  });
  