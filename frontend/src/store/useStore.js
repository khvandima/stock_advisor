import { create } from 'zustand'

const useStore = create((set) => ({
    token: localStorage.getItem('token') || null,
    user: null,

    setToken: (token) => {
        localStorage.setItem('token', token)
        set({ token })
    },

    logout: () => {
        localStorage.removeItem('token')
        set({ token: null, user: null })
    },
}))

export default useStore