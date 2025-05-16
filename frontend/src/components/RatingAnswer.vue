—————<script setup lang="ts">
import { ref } from 'vue' 
import { apiSendRating } from '../api/rating'

const props = defineProps({ 
  question: String,
  sql: String,
  db_response: String,
  explanation: String,
  user_Id: Number
})

const emit = defineEmits(['new_rating_created']);

const q_interpretation = ref(0.5);
const sql_value = ref(0.5);
const isTransmittingRating = ref(false);

const handleSendRating = () => {
    const q = props.question || ''
    const sql  = props.sql || ''
    const db_res = props.db_response || ''
    const expl = props.explanation || ''
    const user_ID = props.user_Id || 0
    sendRating(q, sql, db_res, expl, user_ID, q_interpretation.value, sql_value.value)
}

const mapDigitToWord = (decimal: number)=> {
  const digit = decimal * 100;
  let output = ''
  if(digit == 0){
      output = 'totally not';
    }
  if(digit <= 10 && digit > 0){
      output = 'just a tiny bit';
  }
  if(digit <= 20 && digit > 10){
      output = 'there is something there...';
  }
  if(digit <= 30 && digit > 20){
      output = 'a glympse of it';
  }
  if(digit <= 40 && digit > 30){
      output = 'nearly medium';
  }
  if(digit <= 50 && digit > 40){
      output = 'ok';
  }
  if(digit <= 60 && digit > 50){
      output = 'better than average';
  }
  if(digit <= 70 && digit > 60){
      output = 'quite good';
  }
  if(digit <= 80 && digit > 70){
      output = 'good';
  }
  if(digit <= 90 && digit > 80){
      output = 'nearly perfect';
  }
  if(digit <= 100 && digit > 90){
      output = 'perfect';
  }
  return output
}


const sendRating = async(question: string, sql: string, db_response:string, explanation:string, user_ID: number, q_interpretation: number, sql_quality: number) => {
      isTransmittingRating.value = true;
      try {
          const response = await apiSendRating(question, sql, db_response, explanation, user_ID, q_interpretation, sql_quality);
          isTransmittingRating.value = false;
          console.log(response.status);
          if(response.status == 200){
            emit('new_rating_created');
          }
      } catch (err) {
          console.log(err);
      }
}


</script>

<template>
  <div>
    <h3>Rating</h3>
    <p>- please rate the sql query generation -</p>
    <form>
        <div class="rating-item">
            <label>Understands the question </label>
            <input v-model="q_interpretation" type="range" id="rating_understanding" name="rating_understanding" min="0" max="1" step="0.1"/>
            <div>{{ mapDigitToWord(q_interpretation) }} </div>
        </div>
        <div class="rating-item">
            <label>quality of the sql</label>
            <input v-model="sql_value" type="range" id="rating_understanding" name="rating_understanding" min="0" max="1" step="0.1"/>
            <div>{{ mapDigitToWord(sql_value) }} </div>
        </div>
        <button @click.prevent="handleSendRating()">
          <span v-if="!isTransmittingRating">senden</span>
          <span v-if="isTransmittingRating">sendet</span>
        </button>
    </form>
  </div>
</template>

<style scoped>
#rating_wrapper{
  width: 100%;
}

input[type="range"]::-webkit-slider-runnable-track {
  background: var(--color-foreground);
  border-radius: 4px;
  height: 0.5rem;
}

input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 10px;
  height: 10px;
  margin-top:-4px;
  cursor: ew-resize;
  background: darkblue;
  background-color: darkblue;
  opacity: 0.9;
}

label { display: block}

.rating-item { 
  margin-bottom: 15px;
}

@media (min-width: 1024px) {
  
}
</style>
