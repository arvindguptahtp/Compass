export default {
    name: "modal",
    props: {
        moreLabel: {
            default: "More"
        }
    },
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

        release_relative () {
            console.log(this.$parent)
        },

        body_lock () {
            let body_style = document.getElementsByTagName("body")[0].style;

            // safeguard
            body_style.width = "100%";

            if (!this.show) {
                body_style.overflow = "";
                body_style.position = "";
            }
            else {
                body_style.overflow = "hidden";
                body_style.position = "fixed";
            }
        }
    },
    // beforeMount () {
    //     let bp = "(min-width: 768px)";

    //     if (window.matchMedia(bp).matches) {
    //         this.show_mobile_layout = true;
    //         this.bodyLock();
    //     }
    // },
}
