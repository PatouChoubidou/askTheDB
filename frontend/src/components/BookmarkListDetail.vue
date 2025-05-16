<script setup lang="ts">

const props = defineProps(['bookmark'])

</script>

<template>
   <div class="bookmark-list-detail">
      <div>
        <label>id</label>
        <div>{{ props.bookmark['bookmark_ID'] }}</div>
      </div>
      <div>
        <label>question</label>
        <div>{{ props.bookmark['question'] }}</div>
      </div>
      <div>
        <label>sql</label>
        <div class="code"> {{ props.bookmark['sql'] }}</div>
      </div>
      <div>
        <label>created</label>
        <div>{{ props.bookmark['created_at'] }}</div>
      </div>
   </div>
</template>

<style scoped>

.bookmark-list-detail{
  padding: 20px;
  width: 500px;
}

.bookmark-list-detail > div{
  display: flex;
  align-items: center;
}

.bookmark-list-detail > div:nth-child(3){
  padding:15px 0;
}

.bookmark-list-detail > div:nth-child(4){
  font-size: 0.8rem;
}

.bookmark-list-detail > div > label{
  min-width: 100px;
  font-weight: 600;
  font-size: 0.8rem;
}

.code {
  font-family: monospace;
  font-size: 0.7rem;
  font-weight: 600;
  background-color: rgba(224, 219, 219, 0.9);
  border-radius: 4px;
  padding: 8px 10px 8px 10px;
}

</style>