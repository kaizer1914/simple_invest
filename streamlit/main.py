import streamlit

from vtb.position_report import PositionReport

position_report = PositionReport()
upload = streamlit.file_uploader('Upload')
if upload is not None:
    data = position_report.save_to_db(upload.getvalue())
    streamlit.write(data)

