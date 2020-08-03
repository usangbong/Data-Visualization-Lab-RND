using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeColor : MonoBehaviour
{
    MaterialManager matManager;

    int cnt;

    void Start()
    {
        matManager = GameObject.Find("MaterialManager").GetComponent<MaterialManager>();
        cnt = -1;
    }

    void RandomValue()
    {
        float num = Random.value * 1000;
        cnt = System.Convert.ToInt32(num);
        cnt = cnt % 17;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        { 
            RandomValue();
            gameObject.GetComponent<MeshRenderer>().material = matManager.matList[cnt];
        }
    }
}
