—————<script setup lang="ts"></script>

<template>
  <div id="waiting_wrapper">
    <div id="img_wrapper">
      <img src="../assets/llm_thinks.svg" />
    </div>
   <div>Am I thinking?</div>
</div>
</template>

<style scoped>

#waiting_wrapper {
    background: var(--color-background);
    z-index: 10;
    width: 200px;
    height: 200px;
    padding:10px;
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    border: solid 5px var(--color-foreground);
}

#img_wrapper {
    width: auto;
    display: block;
}

#img_wrapper > img {
    transform-origin: center;
    animation-name: wackeldackel;
    animation-duration: 2s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
    width: 80px;
    height: auto;
}

@keyframes wackeldackel {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(10deg); }
  50% { transform: rotate(0eg); }
  75% { transform: rotate(-10deg); }
  100% { transform: rotate(0deg); }
}
</style>


