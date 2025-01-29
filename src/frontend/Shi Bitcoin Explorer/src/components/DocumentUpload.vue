<template>
  <div class="document-upload">
    <h3>Upload Document</h3>
    <textarea v-model="documentText" placeholder="Enter your document text"></textarea>
    <button @click="uploadDocument" :disabled="!documentText || isUploading">
      {{ isUploading ? 'Uploading...' : 'Upload Document' }}
    </button>
    <p v-if="fileHash">
      Document Hash: <code>{{ fileHash }}</code>
    </p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { sha256 } from 'crypto-hash'

export default {
  data() {
    return {
      documentText: '',
      fileHash: '',
      isUploading: false,
      error: '',
    }
  },
  methods: {
    async uploadDocument() {
      if (!this.documentText) {
        this.error = 'Please enter document text.'
        return
      }

      this.isUploading = true
      this.error = ''

      try {
        // Generate SHA-256 hash of the document
        this.fileHash = await sha256(this.documentText)

        // Send the document and hash to the backend
        const response = await fetch('/reg/upload', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            document: this.documentText,
            document_hash: this.fileHash,
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

textarea {
  width: 100%;
  height: 100px;
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
