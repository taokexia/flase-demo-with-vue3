import { VNode, createVNode, render } from "vue";
import Toast from "../components/Toast.vue";

let toastDiv: VNode;
export function showToast(message: string, type = 'info', time = 2000) {
  if (!toastDiv) {
    toastDiv = createVNode(Toast);
    render(toastDiv, document.body)
  }

  toastDiv.component?.exposed?.show(message, type, time)
}
