using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeTemp : MonoBehaviour
{
    private management Manager;

    private Color baseColor;
    private Color hoverColor;
    private Color clickColor;
    
    private void Start()
    {
        Manager = GameObject.Find("Manager").GetComponent<management>();

        baseColor = Manager.baseColor;
        hoverColor = Manager.hoverColor;
        clickColor = Manager.clickColor;
    }

    private void OnMouseEnter()
    {
        transform.GetComponent<MeshRenderer>().material.color = hoverColor;
        Manager.selectCell = gameObject;
    }

    private void OnMouseExit()
    {
        transform.GetComponent<MeshRenderer>().material.color = baseColor;
        Manager.selectCell = null;
    }

    private void OnMouseDown()
    {
        transform.GetComponent<MeshRenderer>().material.color = clickColor;
    }

    private void OnMouseUpAsButton()
    {
        transform.GetComponent<MeshRenderer>().material.color = hoverColor;
    }
}
