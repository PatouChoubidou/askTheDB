<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import WaitingImg from '../components/WaitingIMG.vue'
import RatingAnswer from '../components/RatingAnswer.vue'
import InputToggle from '../components/InputToggle.vue'
import TableView  from '../components/TableView.vue'
import DbGraphView from '@/components/DbGraphView.vue'
import { useBookmarkStore } from '../stores/bookmark.ts'
import { useTableStore } from '../stores/db_tables.ts'
import { storeToRefs } from 'pinia'
import type { User, Bookmark } from '../interfaces'
import { createBookmark } from '../api/bookmark'
import { apiSendSQL, apiSendQ } from '../api/llm'

const { allBookmarks } = storeToRefs(useBookmarkStore())
// store functions dont need to have state else use computed
const { getBookmarkByUserID } = useBookmarkStore()
const { tables } = storeToRefs(useTableStore())
const { fetchTables } = useTableStore()

// !!! hard corded
const currentUser: User = {
  "user_ID": 1,
  "username": "patrice",
  "email": '',
  "disabled": 0,
  "created_at": '',
}

onMounted(() => {
    fetchTables()
    getBookmarkByUserID(currentUser.user_ID)
})

const question = ref("");
const ratingVisible = ref(false)
const isWaiting = ref(false);
const isViewMagicMode = ref(false)
const isBookmarkMode = ref(false)
const isTableView = ref(false)
const answer = ref({
  question: '',
  sql: 'some SQL',
  column_names: [],
  db_response: 'someRepsonse',
  explanation: 'some Explanation',
  user_ID: currentUser['user_ID']
});
const message = ref('');
 
const showMessage = async (txt: string) => {
    message.value = txt;
    setTimeout(() => {
      message.value = '';
    },  2000);
}

const searchBookmarks = computed((): string[] => {
  let allBookmarkQuestions: string[] = []
  if(question.value === '') {
    return []
  }
  let matches = 0
  let matchLimit = Infinity
  
  allBookmarks.value.filter((bookmark: Bookmark) => {
    const bQuestion: string = bookmark.question
    if( bQuestion.toLowerCase().includes(question.value.toLowerCase() ) && matches < matchLimit ) {
      matches++
      allBookmarkQuestions.push(bQuestion)
    }
  })
  return allBookmarkQuestions
});

const handleMagicModeToggle = () => {
    const currentVal = isViewMagicMode.value;
    isViewMagicMode.value = !currentVal;
}

const handleTableViewToggle = () => {
    const currentVal = isTableView.value;
    isTableView.value = !currentVal;
}

const handleNewRatingCreated = () => {
    showMessage('rating created');
    ratingVisible.value =false;  
};

const handleAskTheDBButton = (q: string) => {
    isBookmarkMode.value = false;
    sendQ(q);
}

const handleUseOwnQuery = () => {
    isBookmarkMode.value = false;
    const q = answer.value["question"]
    const sql = answer.value["sql"]
    sendSQL(q,sql);
}

const handleCreateBookmark = async() => {
    const q = answer.value.question
    const sql = answer.value.sql
    const user_id = currentUser.user_ID
    try{
      const response = await createBookmark(q, sql, user_id);
      if(response){ 
        showMessage("bookmark created");
      }
    }catch(err){
      console.log(err)
    }
    getBookmarkByUserID(currentUser.user_ID)
}

const selectBookmark = (q: string) => {
    isBookmarkMode.value = true
    question.value = q
    sendQ(q);
}

const filterBookmarkFromQuestion = (q: string) => {
  
    let result = {
      'bookmark_ID': 0,
      'question': '',
      'sql': '',
      'user_ID': 0,
      'created_at': ''
    }

    allBookmarks.value.forEach((bookmark) => {
      const bQuestion: string = bookmark.question
      const question: string = q
      if( bQuestion.toLowerCase() == question.toLocaleLowerCase() ) {
        result = bookmark
      }
    })
    console.log(result)
    return result
}

const useBookmarkSQL = async() => {
    const bookmark = filterBookmarkFromQuestion(answer.value['question'])
    const currentQ: string = bookmark['question'] 
    const sql: string = bookmark['sql'] 
    isBookmarkMode.value = true
    await sendSQL(currentQ, sql);
} 
 
const sendQ = async(q: string) => {
    isWaiting.value = true;
    try {
        const response = await apiSendQ(q);
        const json = await response.json();
        console.log(json);
        answer.value = json; 
        question.value = '';
        // ui reaction
        isWaiting.value = false
        ratingVisible.value = true;
        isViewMagicMode.value = true;
     } catch (err) {
        console.log(err);
        showMessage('the error was' + err)
    }
} 

const sendSQL = async(question: string, sql: string) => {
    // activate spinner
    isWaiting.value = true;
    
    try {
        const response = await apiSendSQL(question, sql);
        const json = await response.json();
        answer.value = json; 
        // ui changes
        isWaiting.value = false
        ratingVisible.value =true;
        isViewMagicMode.value = true;
     } catch (err) {
        console.log(err);
        showMessage('the error was' + err)
    }
} 

</script>

<template>
  <main>
  
    <div id="isWaiting" v-if="isWaiting">
      <div id="overlay">
         <WaitingImg />
      </div>
    </div>

    <div v-if="message !== ''">
      <div id="overlay">
         <div id="message">{{ message }}</div> 
      </div>
    </div>
    <DbGraphView></DbGraphView>
    <div id="homeView_wrapper">
      <h2>Ask the DB</h2>
      
      <div id="tablePrint">
        <label>Availlable Tables:</label>
        <p v-if="tables"> {{ tables }}</p>
       
      </div>
  
      <div id="theInput">

        <div class="toggle_wrapper">
          <label>Behind the scenes</label>
          <InputToggle :state=isViewMagicMode @click.prevent="()=> {handleMagicModeToggle()}" />
        </div>
        
        <form id="questionInput">
          <label v-if="answer.question">Question: {{ answer.question }}</label>
          <div>
            <input v-model="question" placeholder="pose question" @click.prevent="()=>{ratingVisible = false; isViewMagicMode = false; answer.explanation='', answer.question=''}"/>
            <button @click.prevent=handleAskTheDBButton(question)>ask the db</button>
          </div>
          <div id="hints">
            <ul v-if="searchBookmarks.length">
              <li>
                Showing {{ searchBookmarks.length }} of {{ allBookmarks.length }} results
              </li>
              <li v-for="bm in searchBookmarks" :key="bm" @click="selectBookmark(bm)">{{ bm }}</li>
            </ul>
          </div>
        </form>

        <div :class="{ active: isViewMagicMode }" id="magicModeWrapper">
          <form id="sqlPrint" >
            <label>Generated SQL</label>
            <textarea v-model=answer.sql></textarea>
            <div class="sqlPrint_func_wrapper">
              <button @click.prevent=handleUseOwnQuery()>use own query</button>
              <button v-if="isBookmarkMode" @click.prevent=useBookmarkSQL()>use <i class="dripicons-bookmark"></i></button>
              <button v-if="!isBookmarkMode" @click.prevent=handleCreateBookmark()>create bookmark</button>
            </div>
          </form>

          <div>
            <label>The Database replied</label>
            <div id="dbResponse" v-if="!isTableView">
              <textarea v-model=answer.db_response disabled></textarea>
            </div>

            <div id="table_view" v-if="isTableView">
              <TableView v-bind:="answer"/>
            </div>

            <div class="toggle_wrapper">
              <label>table view</label>
              <InputToggle :state=isTableView @click.prevent="()=> {handleTableViewToggle()}" />
            </div>
          </div>
        </div><!--end of magic view-->
        <div id="explanation" :class="{ tall: !isViewMagicMode }">
          <label>The LLM's answer:</label>
          <textarea v-model=answer.explanation disabled></textarea>
        </div>
      </div>
    </div> <!--end of the input-->
    <div :class="{ active: !ratingVisible }" id="rating_wrapper">
      <RatingAnswer v-bind:="answer" @new_rating_created="handleNewRatingCreated" />
    </div>
  </main>
</template>

<style scoped>

#message{
  max-width: 320px;
  padding: 10px 20px;
  border: solid 2px var(--color-foreground);
  background-color: var(--color-background);
  border-radius: 4px;
}

#theInput{
  max-width: 580px;
  z-index: 2;
  background-color: var(--color-background);
  padding: 0 4px;
}

#tablePrint{
  display: block;
  max-width: 540px;
}

#tablePrint p{
  font-size: 0.8rem;
}

#magicModeWrapper{
  display: flex;
  flex-direction: column;
  background-color:  var(--my-white--darker);
  border-radius: 8px;
  padding: 0 2%;
  transition: 0.7s all;
  height: 0%; 
  max-width: 540px;
  transform-origin: bottom center;
  overflow: hidden;
}

#magicModeWrapper.active{
  height: 410px; 
  padding: 2% 2%;
}

.toggle_wrapper{
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  align-content: center;
  padding: 10px 0;
}

#rating_wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 350px;
  height: auto;
  z-index: 6;
  background-color:  var(--color-background);
  border: solid 1px var(--color-foreground);
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  position: absolute;
  right: 0;
  top: 0%;
  padding: 30px;
  transition: 1s all;
  transition-delay: 0.5s;
}

#rating_wrapper.active {
  top: -100%;
}

#overlay {
  position: absolute;
  top:0;
  left: 0;
  display: flex;
  align-items: center;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 10;
  background-color: hsla(218, 67%, 13%, 0.3);
}

#homeView_wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  max-height: 100vh;
}

label{display: block;}

input {
  all: unset;
  font-size: 1.2rem;
  padding:  8px 20px;
  min-width: 380px;
  color: var(--color-background);
  background-color: var(--color-foreground);
}

textarea {
  box-sizing: border-box;
  all: unset;
  display: block;
  font-size: 0.8rem;
  padding:  8px 20px;
  min-height: 120px;
  height: auto;
  color: var(--color-background);
  background-color: var(--color-foreground);
  border-radius: 8px;
}

#questionInput, #explanation {
  margin-bottom: 20px;
}

#questionInput {
  width: 100%;
  position: relative;
}

 #hints {
  position: absolute;
  left: 8px;
  z-index: 8;
  background-color: var(--color-background);
  
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  filter: drop-shadow(var(--color-foreground) 0.04rem 0.04rem 0.06rem)
}

#hints ul {
  list-style: none;
  padding: 0;
  max-height: 200px;
  overflow-y: scroll;
  padding: 8px 20px;
}

#hints ul li:not(:first-child)  {
 font-weight: 300;
}

#hints ul li:not(:first-child):hover  {
 color: var(--my-light-up-color);
 cursor: pointer;
 font-weight: 500;
}

#questionInput > div {
  display: flex;
}

#questionInput >div input::placeholder {
  opacity: 0.8;
}

#questionInput input{
  padding:  6px 20px;
  border-bottom-right-radius: 0;
  border-top-right-radius: 0;
  border-bottom-left-radius: 8px;
  border-top-left-radius: 8px;
}

#questionInput button{
  width: 80px;
  border-bottom-right-radius: 8px;
  border-top-right-radius: 8px;
  border-bottom-left-radius: 0;
  border-top-left-radius:0 ;
}

#questionPrint {
  width: 100%;
}

#sqlPrint{ 
  display: flex;
  flex-direction: column; 
}

#sqlPrint > textarea {
  box-sizing: border-box;
  display: block;
  height: auto;
  border-bottom-right-radius: 0px;
}

#sqlPrint > .sqlPrint_func_wrapper {
  align-self:self-end;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

#sqlPrint > .sqlPrint_func_wrapper > button:first-child {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  padding: 4px 20px;
}

#sqlPrint > .sqlPrint_func_wrapper > button:last-child {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-bottom-left-radius: 0;
  padding: 4px 20px;
}

#dbResponse{
 
}

#dbResponse > textarea {
  box-sizing: border-box;
  height: fit-content;
  min-height: 130px;
  width: 100%;
}

#table_view {
  padding: 5px 0;
  display: block;
  width: 100%;
  overflow-x: hidden;
}

#explanation > textarea {
  box-sizing: border-box;
  width: 100%;
  font-size: 1rem;
  min-height: 140px;
  height: fit-content;
  transition: all 1s;
}

#explanation.tall > textarea {
  min-height: 160px;
}

/* mobile first */
@media (min-width: 1024px) {
    #rating_wrapper{
      top: 30%;
    }
  
    #rating_wrapper.active {
    top: -100%;
    } 

    #tablePrint{
      display: none;
    }
}

</style>
