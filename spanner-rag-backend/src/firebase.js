import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCLkm6OOTZLVy00aOFg0g2UbN3bNWluDCA",
  authDomain: "spanner-rag.firebaseapp.com",
  projectId: "spanner-rag",
  storageBucket: "spanner-rag.firebasestorage.app",
  messagingSenderId: "617816068028",
  appId: "1:617816068028:web:4fa6bec4f3317a1a0fa5b9"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();

export const login = () => signInWithPopup(auth, provider);
export const logout = () => signOut(auth);
