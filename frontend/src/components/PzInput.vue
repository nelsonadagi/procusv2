<template>
  <div class="pz-input-wrapper">
    <label v-if="label" :for="inputId" class="pz-input__label">
      <span>{{ label }}</span>
      <span v-if="required" class="pz-input__required" aria-hidden="true">*</span>
    </label>
    <component
      :is="isTextarea ? 'textarea' : 'input'"
      :id="inputId"
      :type="isTextarea ? undefined : inputType"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :rows="isTextarea ? rows : undefined"
      :inputmode="inputmode"
      :min="min"
      :max="max"
      :step="step"
      :autocomplete="autocomplete"
      :class="inputClasses"
      v-bind="attrs"
      @input="handleInput"
    />
    <span v-if="error" class="pz-input__error">{{ error }}</span>
    <span v-else-if="resolvedHint" class="pz-input__hint">{{ resolvedHint }}</span>
  </div>
</template>

<script setup>
  import { computed, useAttrs } from 'vue'

  defineOptions({
    inheritAttrs: false
  })

  const props = defineProps({
    modelValue: [String, Number],
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    placeholder: String,
    disabled: Boolean,
    required: Boolean,
    error: String,
    hint: String,
    helpText: String,
    rows: {
      type: [String, Number],
      default: 4
    },
    inputmode: String,
    min: [String, Number],
    max: [String, Number],
    step: [String, Number],
    autocomplete: String,
    size: {
      type: String,
      default: 'medium'
    }
  })

  const emit = defineEmits(['update:modelValue'])
  const attrs = useAttrs()

  const inputId = `pz-input-${Math.random().toString(36).slice(2, 11)}`
  const isTextarea = computed(() => props.type === 'textarea')
  const inputType = computed(() => (isTextarea.value ? 'text' : props.type))
  const resolvedHint = computed(() => props.helpText || props.hint)

  const inputClasses = computed(() => ({
    'pz-input': true,
    'pz-input--error': props.error,
    [`pz-input--${props.size}`]: true
  }))

  const handleInput = (event) => {
    emit('update:modelValue', event.target.value)
  }
</script>

<style scoped>
  /* Styles mapped entirely into components.css globally */
</style>
