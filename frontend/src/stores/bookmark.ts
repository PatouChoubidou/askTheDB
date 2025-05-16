import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { Bookmark } from '../interfaces'


export const useBookmarkStore = defineStore('bookmark', () => {

    const allBookmarks = ref([] as Bookmark[]);
    const bookmark = ref(null as Bookmark | null)
    const message = ref('');

    const getBookmarks = async() => {
        const url = 'http://127.0.0.1:8000/bookmarks/';
        try {
            const response = await fetch(url);
            const json = await response.json();
            allBookmarks.value = json;
        } catch (err) {
            console.log(err);
            message.value = 'the error was' + err
        }
    }

    const getBookmarkByID = async(id: number) => {
        const url = 'http://127.0.0.1:8000/bookmarks/' + id;
        try {
            const response = await fetch(url);
            const json = await response.json();
            bookmark.value = json;
        } catch (err) {
            console.log(err);
            message.value = 'the error was' + err
        }
    }

    const getBookmarkByUserID = async(user_id: number) => {
        const url = 'http://127.0.0.1:8000/users/' + user_id + '/bookmarks/';
        try {
            const response = await fetch(url);
            const json = await response.json();
            allBookmarks.value = json;
        } catch (err) {
            console.log(err);
            message.value = 'the error was' + err
        }
    }


    const createBookmark = async(question: string, sql: string, user_ID: number) => {
        const url = 'http://127.0.0.1:8000/bookmarks/';
        const payload = {
            "question": question || '',
            "sql": sql || '',
            "user_ID": user_ID || 0
          } 
          const request = new Request(url, {
              method: "POST",
              body: JSON.stringify(payload),
          });
          try {
              const response = await fetch(request);
              // const json = await response.json();
              message.value = 'Bookmark created';
              return response
           } catch (err) {
              console.log(err);
              message.value = 'the error was' + err;
        }
    }

    return { allBookmarks, bookmark, getBookmarks, getBookmarkByUserID, createBookmark, getBookmarkByID, message }
})