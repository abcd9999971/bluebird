/**
 * 組件統一入口文件
 * 提供所有組件的統一導出，便於管理和使用
 */

// 佈局組件
export { default as LeftSidebar } from './layout/LeftSidebar.vue';
export { default as PostsHeader } from './layout/PostsHeader.vue';
export { default as MobileNav } from './layout/MobileNav.vue';
export { default as RightSidebar } from './layout/RightSidebar.vue';
export { default as BottomNavigation } from './layout/BottomNavigation.vue';

// 推文相關組件
export { default as MemberHeader } from './posts/MemberHeader.vue';
export { default as PostList } from './posts/PostList.vue';
export { default as PostItem } from './posts/PostItem.vue';

// 彈窗組件
export { default as PostDetailModal } from './modals/PostDetailModal.vue';
export { default as ProfileModal } from './modals/ProfileModal.vue';
export { default as DateNavModal } from './modals/DateNavModal.vue';

// UI 組件
export { default as Loader } from './ui/Loader.vue';
export { default as ToTopButton } from './ui/ToTopButton.vue';
export { default as ToastNotification } from './ui/ToastNotification.vue';
export { default as TimelineBar } from './ui/TimelineBar.vue';
export { default as PullRefreshIndicator } from './ui/PullRefreshIndicator.vue';
export { default as BirthdayReminder } from './ui/BirthdayReminder.vue';

// 組件分類導出
export const LayoutComponents = {
  LeftSidebar,
  PostsHeader,
  MobileNav,
  RightSidebar,
  BottomNavigation
};

export const PostComponents = {
  MemberHeader,
  PostList,
  PostItem
};

export const ModalComponents = {
  PostDetailModal,
  ProfileModal,
  DateNavModal
};

export const UIComponents = {
  Loader,
  ToTopButton,
  ToastNotification,
  TimelineBar,
  PullRefreshIndicator,
  BirthdayReminder
};
