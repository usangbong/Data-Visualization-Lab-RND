using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReadCSV : MonoBehaviour
{
    public string m_strCSVFileName = string.Empty;



    class TempData

    {

        public int index;

        public string testString;

        public int testInt;

        public float testFloat;

    }



    List<TempData> m_tempData = new List<TempData>();



    // Start is called before the first frame update

    void Start()

    {

        List<Dictionary<string, object>> m_dictionaryData = CSVreader.Read(m_strCSVFileName);



        for (int i = 0; i < m_dictionaryData.Count; i++)

        {

            m_tempData.Add(new TempData());



            m_tempData[i].index = int.Parse((m_dictionaryData[i]["Index"].ToString()));

            m_tempData[i].testString = m_dictionaryData[i]["TestString"].ToString();

            m_tempData[i].testInt = int.Parse(m_dictionaryData[i]["TestInt"].ToString());

            m_tempData[i].testFloat = float.Parse(m_dictionaryData[i]["TestFloat"].ToString());

        }



        for (int i = 0; i < m_tempData.Count; i++)

        {
            Debug.Log("Index : " + m_tempData[i].index + ", TestString : " + m_tempData[i].testString + ", TestInt : " + m_tempData[i].testInt + ", TestFloat : " + m_tempData[i].testFloat);
        }
    }
}
