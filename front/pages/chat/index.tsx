import Head from 'next/head';
import styles from './styles.module.scss';

export default function Chat() {
    return (
        <div className={styles.page}>
            <div className={styles.container}>
                <div className={styles.messagesContainer}>
                    <div className={styles.ownMessage}>jdavnd</div>
                    <div className={styles.otherMessage}>jdavnd</div>
                    <div className={styles.ownMessage}>jdavnd</div>
                </div>
                <input className={styles.messageInput} type="text" placeholder='Digite aqui'/>
            </div>
        </div>
    )
}
    