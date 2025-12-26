/**
 * 組件統一入口文件
 * 提供所有組件的統一導出，便於管理和使用
 */

// 佈局組件
export { default as LayoutLeftSidebar } from './layout/LayoutLeftSidebar.vue';
export { default as LayoutPostsHeader } from './layout/LayoutPostsHeader.vue';
export { default as LayoutMobileNavigation } from './layout/LayoutMobileNavigation.vue';
export { default as LayoutRightSidebar } from './layout/LayoutRightSidebar.vue';
export { default as LayoutBottomNavigation } from './layout/LayoutBottomNavigation.vue';
export { default as AppLayout } from './layout/AppLayout.vue';

// 推文相關組件
export { default as PostMemberHeader } from './posts/PostMemberHeader.vue';
export { default as PostListContainer } from './posts/PostListContainer.vue';
export { default as PostListItem } from './posts/PostListItem.vue';

// 彈窗組件
export { default as PostDetailModal } from './modals/PostDetailModal.vue';
export { default as ProfileModal } from './modals/ProfileModal.vue';
export { default as DateNavigationModal } from './modals/DateNavigationModal.vue';

// UI 組件
export { default as BaseLoader } from './ui/BaseLoader.vue';
export { default as BaseToTopButton } from './ui/BaseToTopButton.vue';
export { default as BaseToastNotification } from './ui/BaseToastNotification.vue';
export { default as BaseTimelineBar } from './ui/BaseTimelineBar.vue';
export { default as BasePullRefreshIndicator } from './ui/BasePullRefreshIndicator.vue';
export { default as BaseBirthdayReminder } from './ui/BaseBirthdayReminder.vue';

// 功能組件
export { default as BaseSearchFeature } from './features/BaseSearchFeature.vue';
export { default as BaseFilterFeature } from './features/BaseFilterFeature.vue';
export { default as BaseNavigationFeature } from './features/BaseNavigationFeature.vue';

// 視圖組件
export { default as TimelineView } from './views/TimelineView.vue';

// 容器組件
export { default as GlobalComponents } from './containers/GlobalComponents.vue';
export { default as AppLogic } from './containers/AppLogic.vue';

// 組件分類導出
export const LayoutComponents = {
  LayoutLeftSidebar,
  LayoutPostsHeader,
  LayoutMobileNavigation,
  LayoutRightSidebar,
  LayoutBottomNavigation,
  AppLayout
};

export const PostComponents = {
  PostMemberHeader,
  PostListContainer,
  PostListItem
};

export const ModalComponents = {
  PostDetailModal,
  ProfileModal,
  DateNavigationModal
};

export const UIComponents = {
  BaseLoader,
  BaseToTopButton,
  BaseToastNotification,
  BaseTimelineBar,
  BasePullRefreshIndicator,
  BaseBirthdayReminder
};

export const FeatureComponents = {
  BaseSearchFeature,
  BaseFilterFeature,
  BaseNavigationFeature
};

export const ViewComponents = {
  TimelineView
};

export const ContainerComponents = {
  GlobalComponents,
  AppLogic
};
