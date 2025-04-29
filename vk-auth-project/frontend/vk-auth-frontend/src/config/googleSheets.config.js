// src/config/googleSheets.config.js

export default {
  // Настройки подключения к Google Sheets
  spreadsheetId: '1QWoH_teqJTcymYwa7H3kljWKyPS5NTLcVSUb9J6otaw', // Заменить на реальный ID таблицы
  tableName: 'test111',
  defaultSheetId: 'sheet1',

  // Настройки бота
  botName: 'phantom-bot@phantombot-433621.iam.gserviceaccount.com',

  // Учетные данные для Google API Service Account
  credentials: {
    type: "service_account",
    project_id: "phantombot-433621",
    private_key_id: "fefadeb67eb960b64d7d45e1983e5f6d7525511c",
    private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCh9/xcEKgn6v6A\nYD3umFPxv3AdGpdoNwEY8se2izSQv68NRTj0JnXM0iqA8rZB8AVega8bMIBWRwUD\nuUeaR6pIERKhC4C72x5DeNG0wbjC+VWAW1Cun4sn8jBql/jfHbzuYmQCoP8Keuxn\nygqbjbjPsWHD7MTzod7OCxfLNkPxDpcb0lrWdOTg31C5Ipl8P2TnzX00vcgHk1O+\nEUQWl2RcW5imjWX7WtUhniYAiF7VEROMwJaf50h/e2OHLezfEp7ZFUEVqwkglJrY\nWgTtasNr7eh11uNkJVT5lFpDTMTuroMnnT2G+Pt277CknXhTFLE8mLZT+1TC+TSh\nGLJUPzvxAgMBAAECggEAB9ZPI5jKPDE8mpNdl8yO3kcWOpBJdHlZ4B5KP9jVRK5D\nvwODFZxBTbV7KUVlQIRHzDp/8bO7eAFEerlFv885K/bIhRqggmaAPMFNO172zNdh\n9d2lRifR5M9NHLFJEWm31TyVTIPEB3qqcvy1nfCB+WnCumdb4dKKrINgpbx01eZ8\nJBjPQQKYXu1ycee45tqrm56+zUSwGO///vuZQLpLaCb3owMeE1f+0li0GawrWMP1\nw39qedQk+hi9e86EJAeU1XTBrd7pXdsQa83CK0DIqYjPdcurZkDMffHxDHJTdnLS\n5eT16WTulmIoKsa3kzyWrDCepqV/54tZbjxhaFx0AQKBgQDiV+rWsscj6YmfxXFm\ngAscADlUfbfFBy5iJ+wMsZfKkGDkxVo69H/2GHPHhXqtxqyPqfsMe5JQvkIaPnzK\nOwcFJDHWeyYtrLEpRBpgLkBkosGbUOAkVkuL1ngPI29zvrsFSUdCLMjDjAkKORZs\nHB9NsGVpDn+TskwcubgzxpAl8QKBgQC3MMp0tFs1XVmOaX3kQjhigy9BOZpCmv3U\nHKbJZVZ0Jr+YoBolL+t6VGmYBRE40QOmFnvghZRtCzlhdVW0WhmtqeboN4S09sj+\nKxNBVCdW9bJunjKKTecgX/RxwxZeg/8hA18RwY22qoKp7+a5EW/XT1kQuUlLdd5z\nZH2yRVJ2AQKBgQCzXdaFI5G6PNTKHy5ZevjSzL6h3SqnYaR5NofSG15dsQKH6Hkz\npRROklwV7gok8f9Hrf17i+WMROmfYIuFuzc59M/l1xuPMH4IZKa+N4jh9zST/4hQ\nY25kt6XW4U7uG2SbsNFeeJz0keGMD2dcbwDDkRkcItgo1C+KyAZYSW9sEQKBgAsV\nQ5pt8vq2jB2Gmlw9+WVUZH6Auql+8Q5tMVYL8IAUfBEC1rIbRRbglobg/5q9Yogg\n4hvCWSmDvVP9IlNIBDeyiMrR2RCNwblG5+JS8hJbyRDSN2KQtgQKaiKb1/Wd7MiV\niKHtYOKFTGR1pDLcMDUJkuzlGN8c4Xl/we8QLJ4BAoGBAJ2lAptxG6cEe/64veV4\nyYtF8PIl2OuDXXxOVubsj4F9i5/CICcHBBT1oX83ZlDDd1p98JI34mjhPILyLD1w\nILX1Ze0egO2P6KRdGQH9Ar/H2xHOPyZRm73TGhAVZQYUOaYXI0Zu7s6vS3nCPQ9D\nUXD0urNI1yrcy4Ru3iUEBVaJ\n-----END PRIVATE KEY-----\n",
    client_email: "phantom-bot@phantombot-433621.iam.gserviceaccount.com",
    client_id: "116457527116560505066",
    auth_uri: "https://accounts.google.com/o/oauth2/auth",
    token_uri: "https://oauth2.googleapis.com/token",
    auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
    client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/phantom-bot%40phantombot-433621.iam.gserviceaccount.com"
  },

  // Настройки отображения
  displaySettings: {
    dataRange: 'A1:Z1000', // Диапазон данных для загрузки
    headerRow: 1,  // Номер строки с заголовками (обычно 1)
    autoRefreshInterval: 60000 // Интервал автообновления в миллисекундах (1 минута)
  }
};
