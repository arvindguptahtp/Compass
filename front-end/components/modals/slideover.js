export default {
    name: "slideover-modal",
    data () {
        return {
            show: false,
            show_mobile_layout: false
        }
    },
    computed: {
        loaded () {
            return this.show;
        }
    },
    methods: {
        toggleModal () {
            this.show = !!!this.show;
            this.release_relative()
            this.body_lock();
        },

        showMobileLayout () {
            this.show_mobile_layout = true;
        },
    },
    // beforeMount () {
    //     let bp = "(min-width: 768px)";

    //     if (window.matchMedia(bp).matches) {
    //         this.show_mobile_layout = true;
    //         this.bodyLock();
    //     }
    // },
}
