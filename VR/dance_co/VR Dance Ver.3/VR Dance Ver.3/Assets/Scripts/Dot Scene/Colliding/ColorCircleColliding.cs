using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorCircleColliding : MonoBehaviour
{
    public GameObject nullParent;
    ColorCircle cCircle;

    private void Start()
    {
        cCircle = GameObject.Find("ColorCircleManager").GetComponent<ColorCircle>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (cCircle.move)
            {
                for (int i = 0; i < other.gameObject.transform.childCount; i++)
                {
                    other.gameObject.transform.GetChild(i).SetParent(nullParent.transform);
                }

                gameObject.transform.SetParent(other.transform);
            }
        }
    }
}
