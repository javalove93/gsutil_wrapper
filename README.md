# gsutil_wrapper

## 사용방법

<pre>
usage: gsutil_wrapper [-h] path_list
</pre>

## path_list 포맷

<pre>
# Options
# 최대로 병렬 실행할 gsutil 개수
# MAX_PROCESSES 100
# MAX_TEMP_STORAGE 100
#
# Samples
# s3://gcs-jerry/ gs://s3-to-gcs-jerry/ -r
# s3://gcs-jerry/xa* gs://s3-to-gcs-jerry/
# s3://gcs-jerry/xb* gs://s3-to-gcs-jerry/
# s3://gcs-jerry/testfolder/ gs://s3-to-gcs-jerry/testfolder/ -r

s3://gcs-jerry/smallfiles/ gs://s3-to-gcs-jerry/smallfiles/ -r
s3://gcs-jerry/* gs://s3-to-gcs-jerry/
s3://gcs-jerry/smallfiles2/ gs://s3-to-gcs-jerry/smallfiles2/ -r

</pre>
