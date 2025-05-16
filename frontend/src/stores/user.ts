import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { User } from '../interfaces'

export const useUserStore = defineStore('user', () => {

    const users = ref([] as User[]);
    const user = ref(null as User | null)
    const error = ref('');

    const fetchUsers = async() => {
        const url = 'http://127.0.0.1:8000/users/';
        try {
            const response = await fetch(url);
            const json = await response.json();
            users.value = json;
        } catch (err) {
            console.log(err);
            error.value = 'the error was' + err
        }
    }

    const fetchUserById = async(id: number) => {
        const url = 'http://127.0.0.1:8000/users/' + id;
        try {
            const response = await fetch(url);
            const json = await response.json();
            user.value = json;
        } catch (err) {
            console.log(err);
            error.value = 'the error was' + err
        }
    }


    return { users, user, error, fetchUsers, fetchUserById}
})