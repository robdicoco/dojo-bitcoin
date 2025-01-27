<template>
  <div class="document-upload">
    <h3>Upload Document</h3>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadDocument" :disabled="!file || isUploading">
      {{ isUploading ? 'Uploading...' : 'Upload Document' }}
    </button>
    <p v-if="fileHash">
      File Hash: <code>{{ fileHash }}</code>
    </p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { sha256 } from 'crypto-hash'

export default {
  data() {
    return {
      file: null,
      fileHash: '',
      isUploading: false,
      error: '',
    }
  },
  methods: {
    async handleFileUpload(event) {
      this.file = event.target.files[0]
      const fileBuffer = await this.file.arrayBuffer()
      this.fileHash = await sha256(fileBuffer)
    },
    async uploadDocument() {
      if (!this.file) {
        this.error = 'Please select a file to upload.'
        return
      }

      this.isUploading = true
      this.error = ''

      try {
        const response = await fetch('/api2/upload', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            fileHash: this.fileHash,
            fileName: this.file.name,
          }),
        })

        if (!response.ok) {
          throw new Error('Failed to upload document.')
        }

        const data = await response.json()
        this.$emit('document-uploaded', data) // Emit event with response data
      } catch (err) {
        this.error = err.message || 'An error occurred during upload.'
      } finally {
        this.isUploading = false
      }
    },
  },
}
</script>

<style scoped>
.document-upload {
  margin-bottom: 2rem;
}

input[type='file'] {
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: var(--button-bg-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: var(--button-hover-bg-color);
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: var(--error-color);
  margin-top: 1rem;
}
</style>
