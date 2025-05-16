<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBookmarkStore } from '../stores/bookmark'
import { storeToRefs } from 'pinia'
import type { User, Bookmark } from '../interfaces'
import BookmarkListDetail from '../components/BookmarkListDetail.vue'
import {deleteBookmarkByID} from '../api/bookmark'

const { allBookmarks } = storeToRefs(useBookmarkStore())

//store functions dont need to have state else use computed
const { getBookmarkByUserID } = useBookmarkStore()

// !!! hard corded
const currentUser: User = {
  "user_ID": 1,
  "username": "patrice",
  "email": '',
  "disabled": 0,
  "created_at": '',
}

onMounted(() => {
    getBookmarkByUserID(currentUser.user_ID)
})

const handleDeleteByID = async(id: number) => {
    if (confirm('Are you sure you want to delete this bookmark?')) {
        await deleteBookmarkByID(id);
        await getBookmarkByUserID(currentUser.user_ID);
    } else {
    // Do nothing!
        console.log('abort delte bookmark');
    }
    
    
}


</script>

<template>
  <main>
    <div id="bookmark-list-wrapper">
        <h2>Bookmark List</h2>
        <ul id="bookmark-list">
            <li class="bookmark-list__item" v-for="b in allBookmarks" v-bind:key="b.bookmark_ID">
                <BookmarkListDetail :bookmark="b"/>
                <div class="bookmark-list__icon-wrapper">
                    <button @click.prevent="handleDeleteByID(b.bookmark_ID)"><i class="dripicons-trash"></i></button>
                </div>
                
            </li>
        </ul>
   </div>
  </main>
</template>

<style scoped>

#bookmark-list-wrapper{
    display: flex;
    flex-direction: column;
    max-width: 600px; 
    margin: 0 auto;
    align-items: center;
}

#bookmark-list{
    list-style: none;
}

#bookmark-list > li {
    display: flex;
    
    border-bottom: solid 1px var(--color-foreground);
}
.bookmark-list__icon-wrapper{
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    flex-wrap: wrap;
    flex-direction: column;
}

.bookmark-list__item__wrapper{
    width: 500px;
}




/* mobile first */
@media (min-width: 1024px) {

}

</style>
