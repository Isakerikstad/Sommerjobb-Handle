<!-- @/views/ProjectView.vue -->
<template>
  <TheNavbar />
  <header class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
    <h1 v-if="loading" class="text-3xl font-bold leading-tight tracking-tight text-gray-900">Loading...</h1>
    <h1 v-else class="text-3xl font-bold leading-tight tracking-tight text-gray-900">{{ stream.name }}</h1>
  </header>
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col space-y-8">
    <iframe :src="streamUrl" v-if="streamUrl" width="100%" height="500vh" frameborder="0"></iframe>
  </main>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useQuery } from '@urql/vue'
import { ref, onMounted, computed } from 'vue'
import { streamQuery } from '@/graphql/queries/stream'
import TheNavbar from '@/components/TheNavbar.vue'


const route = useRoute()
const streamId = route.params.streamId

const streamUrl = ref('')
const loading = ref(true) // new loading state

const { data, fetching, error } = useQuery({
query: streamQuery,
variables: { id: streamId },
})

const stream = computed(() => {
if (!data.value) return null
loading.value = false // set loading to false when data is ready
return data.value.stream
})

onMounted(async () => {
  console.log(data.value)
  console.log(error.value)
  console.log(fetching.value)
  if (data.value) {
    streamUrl.value = `https://speckle.xyz/embed?stream=${streamId}`
  }
})
</script>