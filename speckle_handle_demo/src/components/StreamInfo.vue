<template>
    <div class="border p-8 rounded-lg" v-if="selectedStream">
      <h2>{{ selectedStream.name }}</h2>
      <p>Commits Count: {{ selectedStream.commitsCount }}</p>
      <div>
        <h3>Contributors:</h3>
        <ul>
          <li v-for="contributor in selectedStream.contributors" :key="contributor.id">
            {{ contributor.name }}
          </li>
        </ul>
      </div>
      <div>
        <h3>Comments:</h3>
        <ul>
          <li v-for="comment in selectedStream.comments" :key="comment.id">
            {{ comment.text }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  export interface StreamInfoProps {
    selectedStream: {
      id: string
      name: string
      commitsCount: number
      contributors: { id: string, name: string }[]
      comments: { id: string, text: string }[]
    }
  }
  
  defineProps<StreamInfoProps>()
  </script>