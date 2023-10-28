import axios from 'axios'
import data from "bootstrap/js/src/dom/data";

const apiClient = axios.create({
    baseURL: '/api',
});

function setToken() {
    let token = localStorage.getItem('token');
    if (token) {
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
}


const server = {
    async login(data) {
        return await apiClient.post('/auth/login', data);
    },
    async register(data) {
        return await apiClient.post('/auth/register', data);
    },
    async getUserInfo() {
        setToken();
        return await apiClient.get('/users/my_info');
    },
    async updateUserInfo(data) {
        setToken();
        return await apiClient.put('/users/update_info/', data);
    },
    async getCourseList(page = 1) {
        setToken();
        return await apiClient.get('/courses', {
            params: {
                page: page
            }
        });
    },
    async getCourseDetail(course_id) {
        return await apiClient.get(`/courses/${course_id}/`);
    },
    async createPost(data) {
        setToken();
        return await apiClient.post('/posts/', data);
    },
    async getPostList(page = 1) {
        return await apiClient.get(`/posts/?page=${page}`);
    },
    async searchPostList(keyword, page = 1) {
        return await apiClient.get(`/posts/?search=${keyword}&page=${page}`);
    },
    async getPostDetail(postId) {
        return await apiClient.get(`/posts/${postId}/`);
    },
    async getReplyList(postId) {
        return await apiClient.get(`/replies/?post=${postId}`);
    },
    async createReply(data) {
        setToken();
        return await apiClient.post('/replies/', data);
    },
    async generateStudyPlan() {
        setToken();
        return await apiClient.get(`/studyplan`);
    },
    async enrollCourse(courseId) {
        setToken();
        return await apiClient.post(`/courses/${courseId}/enroll/`);
    },
    async getQuiz(quizId) {
        return await apiClient.get(`/quizzes/${quizId}/`);
    },
    async dropCourse(courseId) {
        setToken();
        return await apiClient.post(`/courses/${courseId}/drop/`);
    },
    async getDashboard() {
        setToken();
        return await apiClient.get('/dashboard');
    },
    async createChat(data) {
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.body;
    }
}

export default server;
