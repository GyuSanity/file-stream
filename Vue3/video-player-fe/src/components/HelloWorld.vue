<template>
  <div class="video-container">
    <div class="videos">
      <video
        v-for="(url, index) in videoUrls"
        :key="index"
        ref="videoRefs"
        :src="url"
        @loadedmetadata="onLoadedMetadata"
        @timeupdate="onTimeUpdate"
        :muted="true"
        playsinline
        controls
      />
    </div>

    <input
      type="range"
      min="0"
      :max="duration"
      step="0.1"
      v-model="currentTime"
      @input="onSeek"
    />

    <button @click="togglePlay">
      {{ isPlaying ? "⏸ Pause All" : "▶ Play All" }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'

const videoUrls = [
  'http://localhost:8000/video/test1.mp4',
  'http://localhost:8000/video/test1.mp4',
  'http://localhost:8000/video/test1.mp4',
]

const videoRefs = ref<HTMLVideoElement[]>([])
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const isSeeking = ref(false)

const togglePlay = () => {
  videoRefs.value.forEach(video => {
    if (isPlaying.value) {
      video.pause()
    } else {
      video.play()
    }
  })
  isPlaying.value = !isPlaying.value
}

const onSeek = () => {
  isSeeking.value = true
  videoRefs.value.forEach(video => {
    video.currentTime = currentTime.value
  })
}

const onTimeUpdate = () => {
  if (!isSeeking.value) {
    // 아무 비디오 하나 기준으로 동기화
    const current = videoRefs.value[0]?.currentTime ?? 0
    currentTime.value = current
  }
}

const onLoadedMetadata = () => {
  // 모든 비디오가 로드된 후 가장 짧은 duration을 기준으로 설정
  const durations = videoRefs.value.map(v => v.duration).filter(Boolean)
  duration.value = Math.min(...durations)
}

onMounted(() => {
  // 영상 엘리먼트 수동 등록
  videoRefs.value = Array.from(
    document.querySelectorAll('video')
  ) as HTMLVideoElement[]
})
</script>

<style scoped>
.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.videos {
  display: flex;
  gap: 10px;
  justify-content: center;
}

video {
  width: 300px;
  height: auto;
}
</style>
