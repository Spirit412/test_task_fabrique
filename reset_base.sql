delete from users where true;
delete from clients where true;
delete from mailings where true;
delete from messages where true;
delete from logs_clients where true;
delete from logs_mailings where true;
delete from logs_messages where true;


ALTER SEQUENCE api_user_tokens_id_seq RESTART WITH 1;
ALTER SEQUENCE clients_id_seq RESTART WITH 1;
ALTER SEQUENCE mailings_id_seq RESTART WITH 1;
ALTER SEQUENCE messages_id_seq RESTART WITH 1;
ALTER SEQUENCE logs_clients_id_seq RESTART WITH 1;
ALTER SEQUENCE logs_mailings_id_seq RESTART WITH 1;
ALTER SEQUENCE logs_messages_id_seq RESTART WITH 1;

