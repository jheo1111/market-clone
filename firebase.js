import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";
import {getAuth} from "firebase/auth";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object

const firebaseConfig = {
  apiKey: "AIzaSyAe1Fe0Gv-7HSYBp6fNX_GBtjQWj1xHufg",
  authDomain: "carrot-market-efea6.firebaseapp.com",
  databaseURL: "https://carrot-market-efea6-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "carrot-market-efea6",
  storageBucket: "carrot-market-efea6.appspot.com",
  messagingSenderId: "1068398020151",
  appId: "1:1068398020151:web:ec335765d43cd6a689e1b2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);
const storage = getStorage(app);
const auth = getAuth(app);