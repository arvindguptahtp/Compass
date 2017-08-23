export default {
    name: "slideover-modal",
    data () {
        return {
            show: false
        }
    },
    computed: {
        loaded () {
            return this.show
        }
    },
    methods: {
        toggle_modal () {
            this.show = !!!this.show
        },
    }
}
