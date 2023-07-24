// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCNe7oeNt_bmoQ0DkkDF_KKYa5_thxYVP8",
  authDomain: "housefire-a6205.firebaseapp.com",
  projectId: "housefire-a6205",
  storageBucket: "housefire-a6205.appspot.com",
  messagingSenderId: "475012886748",
  appId: "1:475012886748:web:81922c1c3f172e2521c419",
  measurementId: "G-27LZP68SQ7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);