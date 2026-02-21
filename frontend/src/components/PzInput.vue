<template>
  <div class="pz-input-wrapper">
    <label v-if="label" :for="inputId" class="pz-input__label">
      {{ label }}
    </label>
    <input :id="inputId" :type="type" :value="modelValue" :placeholder="placeholder" :disabled="disabled"
      :class="inputClasses" @input="$emit('update:modelValue', $event.target.value)" />
    <span v-if="error" class="pz-input__error">{{ error }}</span>
    <span v-else-if="hint" class="pz-input__hint">{{ hint }}</span>
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    modelValue: String,
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    placeholder: String,
    disabled: Boolean,
    error: String,
    hint: String,
    size: {
      type: String,
      default: 'medium'
    }
  })

  defineEmits(['update:modelValue'])

  const inputId = computed(() => `pz-input-${Math.random().toString(36).substr(2, 9)}`)

  const inputClasses = computed(() => ({
    'pz-input': true,
    'pz-input--error': props.error,
    [`pz-input--${props.size}`]: true
  }))
</script>

<style scoped>
  /* Styles mapped entirely into components.css globally */
</style>
