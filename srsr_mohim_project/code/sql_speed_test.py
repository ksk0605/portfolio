import time
import psycopg2  # PostgreSQL용 라이브러리
import pymysql   # MySQL용 라이브러리

def execute_query_multiple_times(conn, query, num_executions):
    """
    주어진 쿼리를 여러 번 실행하고 평균 실행 시간을 계산.
    
    :param conn: 데이터베이스 연결 객체
    :param query: 실행할 SQL 쿼리
    :param num_executions: 실행 횟수
    :return: 평균 실행 시간 (초)
    """
    total_time = 0
    for _ in range(num_executions):
        start_time = time.time()
        with conn.cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()  # 결과 가져오기
        end_time = time.time()
        total_time += (end_time - start_time)
    
    avg_time = total_time / num_executions
    return avg_time

def main():
    # 데이터베이스 연결 정보 설정
    postgresql_config = {
        "dbname": "postgres",
        "user": "sungkyum",
        "host": "localhost",
        "port": 5432
    }

    mysql_config = {
        "host": "localhost",
        "user": "root",
        "database": "json_test",
        "port": 3306
    }

    # 테스트할 쿼리와 실행 횟수
    pg_query = "SET search_path TO json_test; SELECT * FROM church_member WHERE custom_properties->>'membershipLevel' = 'gold';"
    mysql_query = "SELECT * FROM church_member WHERE JSON_EXTRACT(custom_properties, '$.membershipLevel') = 'gold';"
    num_executions = 10

    # PostgreSQL 테스트
    with psycopg2.connect(**postgresql_config) as pg_conn:
        # search_path를 설정 후 쿼리 실행
        with pg_conn.cursor() as cursor:
            cursor.execute("SET search_path TO json_test;")
        pg_avg_time = execute_query_multiple_times(pg_conn, pg_query, num_executions)
        print(f"PostgreSQL 평균 실행 시간: {pg_avg_time:.5f}초 ({num_executions}회 실행)")

    # MySQL 테스트
    with pymysql.connect(**mysql_config) as mysql_conn:
        mysql_avg_time = execute_query_multiple_times(mysql_conn, mysql_query, num_executions)
        print(f"MySQL 평균 실행 시간: {mysql_avg_time:.5f}초 ({num_executions}회 실행)")

if __name__ == "__main__":
    main()
