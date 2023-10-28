<template>
  <main class="container py-3 d-flex flex-column align-items-center">
    <div style="width: 800px">
      <strong class="mb-3 fs-4">{{quiz.name}}</strong>
      <div class="text-muted fs-6 mb-4">{{quiz.description}}</div>
      <div v-for="(question, index) in questions" :key="index" class="mb-4">
        <p>{{ index + 1 }}. {{ question.text }}</p>
        <div v-for="(option, oIndex) in question.options" :key="oIndex" class="form-check">
          <input class="form-check-input" type="radio" :name="'question-' + index" :value="option"
                 v-model="userAnswers[index]">
          <label class="form-check-label">
            {{ option }}
          </label>
        </div>
        <div v-if="submitted && userAnswers[index] !== question.correctAnswer" class="text-danger">
          Incorrect! Correct answer: {{ question.correctAnswer }}
        </div>
      </div>
      <button @click="submitAnswers" class="btn btn-primary">Submit</button>
    </div>
  </main>

</template>
<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      quiz:{},
      submitted: false,
      userAnswers: [],
      questions: [

      ]

    }
  },
  methods: {
    submitAnswers: function () {
      this.submitted = true;
    }
  },
  mounted() {
    const quizId = this.$route.params.quizId
    server.getQuiz(quizId).then(res => {
      this.quiz = res.data
      this.questions = res.data.questions
    })
  }
}
</script>
