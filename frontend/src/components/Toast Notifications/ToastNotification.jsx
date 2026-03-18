import React, { useEffect, useState, memo, useCallback } from "react";

/* Styling */
import styles from "./ToastNotification.module.css";
import '../../styles/Theme.css';

/* ============================================================================
 * TOAST NOTIFICATION COMPONENT
 * ============================================================================
 * Individual toast notification with auto-dismiss and manual close
 * ============================================================================
 */

const ToastNotification = memo(({ id, type = "info", title, message, errorCode, onClose }) => {
  // ========================================
  // STATE MANAGEMENT
  // ========================================
  const [isClosing, setIsClosing] = useState(false);

  // ========================================
  // EFFECTS - Auto-dismiss timer
  // ========================================
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsClosing(true);
      setTimeout(() => {
        onClose(id);
      }, 300);
    }, 5000);

    return () => clearTimeout(timer);
  }, [id, onClose]);

  // ========================================
  // EVENT HANDLERS
  // ========================================
  const handleClose = useCallback(() => {
    setIsClosing(true);
    setTimeout(() => {
      onClose(id);
    }, 300);
  }, [id, onClose]);

  // ========================================
  // RENDER
  // ========================================
  return (
    <div className={`${styles.toast} ${styles[type]} ${isClosing ? styles.closing : ''}`}>
      <div className={styles.toastContent}>
        {title && <div className={styles.toastTitle}>{title}</div>}
        <div className={styles.toastMessage}>{message}</div>
        {errorCode && <div className={styles.toastCode}>Code: {errorCode}</div>}
      </div>
      <button className={styles.closeButton} onClick={handleClose} aria-label="Close notification">
        ×
      </button>
    </div>
  );
}, (prevProps, nextProps) => {
  return (
    prevProps.id === nextProps.id &&
    prevProps.type === nextProps.type &&
    prevProps.title === nextProps.title &&
    prevProps.message === nextProps.message &&
    prevProps.errorCode === nextProps.errorCode &&
    prevProps.onClose === nextProps.onClose
  );
});

ToastNotification.displayName = "ToastNotification";

export default ToastNotification;