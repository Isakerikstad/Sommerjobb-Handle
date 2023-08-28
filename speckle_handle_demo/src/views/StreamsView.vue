<!-- @/views/StreamViews.vue -->
<template>
  <TheNavbar />
  <header class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
    <h1 class="text-3xl font-bold leading-tight tracking-tight text-gray-900">Prosjekter</h1>
  </header>
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col space-y-8">
    <StreamSearchBar v-model="searchQuery" />
    <StreamGrid :streams="streams" :error="error" :fetching="fetching" @stream-clicked="handleStreamClick" />
    <iframe src="https://speckle.xyz/embed?stream=4d80493af0" width="600" height="400" frameborder="0"></iframe> 

  </main>
</template>

<script setup lang="ts">
import StreamGrid from '@/components/StreamGrid.vue'
import type { StreamGridItemProps } from '@/components/StreamGridItem.vue'
import TheNavbar from '@/components/TheNavbar.vue'
import StreamSearchBar from '@/components/StreamSearchBar.vue'
import { streamsQuery } from '@/graphql/queries/streams'
import { useQuery } from '@urql/vue'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'


const searchQuery = ref('')
const selectedStreamId = ref('')

const { data, error, fetching } = useQuery({
  query: streamsQuery,
  variables: { searchQuery }
})

const streams = computed<StreamGridItemProps[]>(() => {
  if (!data.value) return []
  return data.value.streams.items.map((stream: any) => ({
    id: stream.id,
    name: stream.name,
    commitsCount: stream.commits.totalCount
  }))
})

const selectedStreamUrl = computed(() => selectedStreamId.value ? `https://speckle.xyz/embed?stream=${selectedStreamId.value}` : '')

const router = useRouter()

const handleStreamClick = (streamId: string) => {
  router.push({ name: 'projectview', params: { streamId } })
}


</script>
