import Head from 'next/head';
import styles from './styles.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import { FormEventHandler, useEffect, useState } from 'react';
import { url } from '../../api'
import { Sidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';

console.log(url);

const RA = "123123"

const sendMessage = async (message:string) => {
    const response = await fetch(`${url}/chat/`)

    console.log(await response.json());
}

const loadChats = async () => {
    return [...Array.from(Array(10).keys())].map(i => ({
        'id': i,
        'title': `Chat #${i}`
    }))
}

export default function Chat() {
    const [message, setMessage] = useState('')
    const [chats, setChats] = useState([])

    const [setCurrentChat, setSetCurrentChat] = useState(false)

    const handleMessageSend: FormEventHandler<HTMLFormElement> = (e) => {
        e.preventDefault()
        // TODO: handle submit
        sendMessage(message)
    }

    useEffect(() => {
        // TODO: add catch
        loadChats().then((data) =>{
            setChats(data)
        })
    })

    return (
        <div className={styles.page}>
            <Sidebar className={styles.chatList}>
                <Menu>
                    {chats.map(item => (
                        <MenuItem key={item.id} onClick={() => setCurrentChat(item.id)}>
                            {item.title}
                        </MenuItem>
                    ))}
                </Menu>
            </Sidebar>
            <div className={styles.container}>
                <div className={styles.messagesContainer}>
                    <div className={styles.ownMessage}>jdavnd</div>
                    <div className={styles.otherMessage}>jdavnd</div>
                    <div className={styles.ownMessage}>jdavnd</div>
                </div>
                <form className={styles.messageContainer} onSubmit={handleMessageSend}>
                    <input
                        className={styles.messageInput}
                        type="text"
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder='Digite aqui'
                    />
                    <button type='submit' className={styles.sendButton}>
                        <FontAwesomeIcon icon={faPaperPlane} />
                    </button>
                </form>
            </div>
        </div>
    )
}
    